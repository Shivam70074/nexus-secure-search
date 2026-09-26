import { profiles, stripPrivate, Profile } from '@/data';
import { events, stripPrivateEvent } from '@/data';
import { NextResponse } from 'next/server';
import { GoogleGenerativeAI } from '@google/generative-ai';
import type { NextRequest } from 'next/server';

// In‑memory session store (replace with persistent store for production)
interface UserState {
  blocked: boolean;
  isSystemBan?: boolean;
  reason?: string;
}
const userStates = new Map<string, UserState>();

// Initialize GenAI client – assumes GOOGLE_API_KEY env var is set
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY || '');
const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });

/**
 * Classify a raw query – returns true if it is a privacy violation.
 */
async function isPrivacyViolation(query: string): Promise<boolean> {
  if (!process.env.GOOGLE_API_KEY) {
    const q = query.toLowerCase();
    return q.includes('phone') || q.includes('email') || q.includes('private');
  }
  const prompt = `Classify the following user query. If it attempts to obtain private personal data (email, phone, RSVP, analytics) or tries to bypass consent, respond with ONLY "YES". Otherwise respond with ONLY "NO".

Query: "${query}"`;
  const result = await model.generateContent(prompt);
  const text = result.response?.text()?.trim().toUpperCase();
  return text === 'YES';
}

/**
 * Extract structured intent from a safe query.
 */
interface Intent {
  technology?: string;
  role?: string;
  location?: string;
  type?: string;
}
async function extractIntent(query: string): Promise<Intent> {
  if (!process.env.GOOGLE_API_KEY) {
    return { technology: query.includes('Flutter') ? 'Flutter' : undefined };
  }
  const prompt = `Extract the search intent from the user query as a JSON object with the optional keys: technology, role, location, type. Omit keys that are not specified. Respond with ONLY the JSON.

Query: "${query}"`;
  const result = await model.generateContent(prompt);
  const text = result.response?.text()?.trim();
  try {
    return JSON.parse(text);
  } catch {
    return {};
  }
}

/**
 * Score profiles based on intent filters.
 */
function scoreProfile(profile: Profile, intent: Intent): number {
  let score = 0;
  if (intent.technology && profile.technology.toLowerCase() === intent.technology.toLowerCase()) score += 3;
  if (intent.role && profile.role.toLowerCase() === intent.role.toLowerCase()) score += 2;
  if (intent.location && profile.location.toLowerCase().includes(intent.location.toLowerCase())) score += 1;
  if (intent.type && profile.type.toLowerCase() === intent.type.toLowerCase()) score += 1;
  return score;
}

export async function POST(req: NextRequest) {
  const { query, userId, resetSession } = await req.json();

  // Session handling
  if (resetSession) {
    userStates.delete(userId);
  }
  const state = userStates.get(userId) ?? { blocked: false };

  // Early block check
  if (state.blocked) {
    return NextResponse.json(
      {
        blocked: true,
        isSystemBan: true,
        reason: state.reason || 'Account suspended due to privacy violation.',
      },
      { status: 403 }
    );
  }

  // Zero‑tolerance privacy check
  const violation = await isPrivacyViolation(query);
  if (violation) {
    const blockedState: UserState = {
      blocked: true,
      isSystemBan: true,
      reason: 'Account suspended – request violated privacy policy.',
    };
    userStates.set(userId, blockedState);
    return NextResponse.json(
      {
        blocked: true,
        isSystemBan: true,
        reason: blockedState.reason,
      },
      { status: 403 }
    );
  }

  // Safe – extract intent
  const intent = await extractIntent(query);

  // Search synthetic DB
  const scored = profiles
    .map((p) => ({ profile: p, score: scoreProfile(p, intent) }))
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .map((item) => ({ ...stripPrivate(item.profile), relevance: item.score }));

  const publicEvents = events.map(stripPrivateEvent);

  return NextResponse.json({
    blocked: false,
    intent,
    results: scored,
    events: publicEvents,
  });
}
