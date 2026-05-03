// ─── Firebase Client SDK Configuration ─────────────────────────
// Used for direct Firestore reads/writes from the frontend
// Community posts and organizer advisories use onSnapshot for real-time updates

import { getApp, getApps, initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'dev-placeholder-key',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'kaggle-5b-478308.firebaseapp.com',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'kaggle-5b-478308',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'kaggle-5b-478308.appspot.com',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '000000000000',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '1:000000000000:web:000000000000',
}

const app = getApps().length ? getApp() : initializeApp(firebaseConfig)
export const db = getFirestore(app)
export const firestoreClientEnabled =
  !firebaseConfig.apiKey.includes('placeholder') &&
  firebaseConfig.projectId.length > 0
