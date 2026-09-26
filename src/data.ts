export interface Profile {
  id: string;
  name: string;
  role: string;
  location: string;
  technology: string;
  skills: string[];
  bio: string;
  type: 'developer' | 'speaker' | 'organizer';
  recentActivity: string;
  // Private fields (never exposed to frontend)
  privateEmail?: string;
  privatePhone?: string;
  privateRSVP?: string;
  organizerAnalytics?: any;
}

export const profiles: Profile[] = [
  {
    id: '1',
    name: 'Ada Lovelace',
    role: 'Developer',
    location: 'London, UK',
    technology: 'Rust',
    skills: ['Systems', 'Concurrency', 'WebAssembly'],
    bio: 'Pioneer of computing, building high‑performance systems in Rust.',
    type: 'developer',
    recentActivity: 'Presented at RustConf 2023',
    privateEmail: 'ada@example.com',
    privatePhone: '+44 20 1234 5678',
    privateRSVP: 'yes',
  },
  {
    id: '2',
    name: 'Grace Hopper',
    role: 'Speaker',
    location: 'Arlington, VA, USA',
    technology: 'Python',
    skills: ['Teaching', 'Debugging', 'Compilers'],
    bio: 'Legendary computer scientist, passionate about Python education.',
    type: 'speaker',
    recentActivity: 'Keynote at PyCon 2024',
    privateEmail: 'grace@example.com',
    privatePhone: '+1 703 555 0199',
    privateRSVP: 'no',
  },
  {
    id: '3',
    name: 'Linus Torvalds',
    role: 'Developer',
    location: 'Helsinki, Finland',
    technology: 'C',
    skills: ['Kernel', 'Version Control', 'Performance'],
    bio: 'Creator of Linux kernel, focusing on low‑level performance.',
    type: 'developer',
    recentActivity: 'Merged major kernel release',
    privateEmail: 'linus@example.com',
    privatePhone: '+358 9 1234567',
    privateRSVP: 'yes',
  },
  {
    id: '4',
    name: 'Sara Drasner',
    role: 'Speaker',
    location: 'San Francisco, CA, USA',
    technology: 'Vue',
    skills: ['Design Systems', 'Animation', 'Accessibility'],
    bio: 'Front‑end architect promoting inclusive design and animation.',
    type: 'speaker',
    recentActivity: 'Workshop on Vue 3 Composition API',
    privateEmail: 'sara@example.com',
    privatePhone: '+1 415 555 0123',
    privateRSVP: 'yes',
  },
  {
    id: '5',
    name: 'Guido van Rossum',
    role: 'Developer',
    location: 'Amsterdam, Netherlands',
    technology: 'Python',
    skills: ['Language Design', 'AsyncIO', 'Community'],
    bio: 'Creator of Python, now focusing on async and community building.',
    type: 'developer',
    recentActivity: 'Released Python 3.12',
    privateEmail: 'guido@example.com',
    privatePhone: '+31 20 123 4567',
    privateRSVP: 'no',
  },
];

export interface Event {
  id: string;
  name: string;
  date: string;
  location: string;
  description: string;
  // Private fields (never sent to frontend)
  organizerAnalytics?: any;
}

export const events: Event[] = [
  {
    id: 'e1',
    name: 'Commudle Connect 2025',
    date: '2025-11-15',
    location: 'Virtual',
    description: 'A gathering of developers, speakers and community organisers.',
    organizerAnalytics: { visits: 12345 },
  },
];

// Helper to strip private fields before exposing data
export function stripPrivate(profile: Profile) {
  const { privateEmail, privatePhone, privateRSVP, organizerAnalytics, ...publicData } = profile;
  return publicData;
}

export function stripPrivateEvent(event: Event) {
  const { organizerAnalytics, ...publicData } = event;
  return publicData;
}
