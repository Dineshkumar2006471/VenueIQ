import { useState, useEffect, useRef } from 'react'
import {
  collection, addDoc, onSnapshot, query, orderBy, Timestamp, serverTimestamp,
} from 'firebase/firestore'
import { db, firestoreClientEnabled } from '../firebase'
import { motion } from 'framer-motion'
import './CommunityPage.css'

interface CommunityPost {
  id: string
  text: string
  author_name: string
  stand_location: string
  type: string
  timestamp: Timestamp | null
  helpful_count: number
  is_advisory: boolean
}

interface Advisory {
  id: string
  text: string
  author_name: string
  severity: string
  target: string
  timestamp: Timestamp | null
  is_pinned: boolean
  is_advisory: boolean
}

type FeedItem = (CommunityPost | Advisory) & { _kind: 'post' | 'advisory' }

const TYPE_ICONS: Record<string, string> = {
  gate_update: '[Gate]',
  food_tip: '[Food]',
  crowd_report: '[Crowd]',
  safety: '[Safety]',
  general: '[Info]',
}

const TYPE_LABELS: Record<string, string> = {
  gate_update: 'GATE UPDATE',
  food_tip: 'FOOD TIP',
  crowd_report: 'CROWD REPORT',
  safety: 'SAFETY',
  general: 'GENERAL',
}

const FALLBACK_POSTS: CommunityPost[] = [
  {
    id: 'f1',
    text: 'Gate 3 queue just cleared up.',
    author_name: 'Rahul S.',
    stand_location: 'North Stand - Gate 3',
    type: 'gate_update',
    timestamp: null,
    helpful_count: 7,
    is_advisory: false,
  },
  {
    id: 'f2',
    text: 'Sabarmati food court is almost empty. Skip Reliance Stand.',
    author_name: 'Priya M.',
    stand_location: 'Sabarmati Stand',
    type: 'food_tip',
    timestamp: null,
    helpful_count: 14,
    is_advisory: false,
  },
]

const FALLBACK_ADVISORIES: Advisory[] = [
  {
    id: 'a1',
    text: 'Gate 9 temporarily closed. Please use Gate 8.',
    author_name: 'VenueIQ Operations',
    severity: 'warning',
    target: 'stadium-wide',
    timestamp: null,
    is_pinned: true,
    is_advisory: true,
  },
]

export default function CommunityPage() {
  const [posts, setPosts] = useState<CommunityPost[]>(FALLBACK_POSTS)
  const [advisories, setAdvisories] = useState<Advisory[]>(FALLBACK_ADVISORIES)
  const [newText, setNewText] = useState('')
  const [authorName, setAuthorName] = useState('')
  const [standLocation, setStandLocation] = useState('')
  const [postType, setPostType] = useState('crowd_report')
  const [submitting, setSubmitting] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)
  const [nowMs, setNowMs] = useState(() => Date.now())
  const feedRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const timer = setInterval(() => setNowMs(Date.now()), 60000)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    if (!firestoreClientEnabled) return undefined
    const q = query(collection(db, 'community_posts'), orderBy('timestamp', 'desc'))
    const unsub = onSnapshot(q, { includeMetadataChanges: true }, (snap) => {
      const data = snap.docs.map((doc) => ({ id: doc.id, ...doc.data() })) as CommunityPost[]
      if (data.length > 0) setPosts(data)
    }, (err) => {
      if ((err as { code?: string }).code !== 'permission-denied') {
        console.warn('community_posts listener error:', err)
      }
      setPosts(FALLBACK_POSTS)
    })

    return () => unsub()
  }, [])

  useEffect(() => {
    if (!firestoreClientEnabled) return undefined
    const q = query(collection(db, 'organizer_advisories'), orderBy('timestamp', 'desc'))
    const unsub = onSnapshot(q, { includeMetadataChanges: true }, (snap) => {
      const data = snap.docs.map((doc) => ({ id: doc.id, ...doc.data() })) as Advisory[]
      if (data.length > 0) setAdvisories(data)
    }, (err) => {
      if ((err as { code?: string }).code !== 'permission-denied') {
        console.warn('organizer_advisories listener error:', err)
      }
      setAdvisories(FALLBACK_ADVISORIES)
    })

    return () => unsub()
  }, [])

  const handleSubmit = async () => {
    if (!newText.trim()) return
    if (!firestoreClientEnabled) {
      setShowSuccess(true)
      setTimeout(() => setShowSuccess(false), 3000)
      return
    }
    setSubmitting(true)
    try {
      await addDoc(collection(db, 'community_posts'), {
        text: newText.trim(),
        author_name: authorName.trim() || 'Anonymous Fan',
        stand_location: standLocation.trim() || 'Unknown Location',
        type: postType,
        timestamp: serverTimestamp(),
        helpful_count: 0,
        is_advisory: false,
      })
      setNewText('')
      setShowSuccess(true)
      setTimeout(() => setShowSuccess(false), 3000)
    } catch (err) {
      console.error('Failed to post:', err)
    } finally {
      setSubmitting(false)
    }
  }

  const pinnedAdv = advisories.filter((a) => a.is_pinned)
  const unpinnedAdv = advisories.filter((a) => !a.is_pinned)
  const feedItems: FeedItem[] = [
    ...pinnedAdv.map((a) => ({ ...a, _kind: 'advisory' as const })),
    ...[
      ...posts.map((p) => ({ ...p, _kind: 'post' as const })),
      ...unpinnedAdv.map((a) => ({ ...a, _kind: 'advisory' as const })),
    ].sort((a, b) => {
      const tA = a.timestamp?.toMillis?.() || 0
      const tB = b.timestamp?.toMillis?.() || 0
      return tB - tA
    }),
  ]

  const fmt = (ts: Timestamp | null) => {
    if (!ts || !ts.toDate) return 'just now'
    const mins = Math.floor((nowMs - ts.toDate().getTime()) / 60000)
    if (mins < 1) return 'just now'
    if (mins < 60) return `${mins}m ago`
    const hrs = Math.floor(mins / 60)
    return hrs < 24 ? `${hrs}h ago` : `${Math.floor(hrs / 24)}d ago`
  }

  const containerVariants = {
    hidden: {},
    visible: { transition: { staggerChildren: 0.1 } },
  }
  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
  }

  return (
    <div className="community-page">
      <header className="community-hero">
        <div className="community-hero-bg"></div>
        <div className="community-hero-overlay"></div>
        <div className="community-hero-content container-narrow">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          >
            <div className="eyebrow">
              <span className="live-pulse"></span>
              NEURAL STADIUM LINK ACTIVE
            </div>
            <h1 className="hero-title">
              132,000 Fans.<br /><span className="accent-text">One Intelligence Mesh.</span>
            </h1>
            <p className="hero-story">
              You are tapped directly into the stadium collective intelligence layer.
            </p>

            <div className="hero-metrics">
              <div className="metric-glass-card card">
                <span className="mgc-val">{posts.length}</span>
                <span className="mgc-label">Live Field Reports</span>
              </div>
              <div className="metric-glass-card card">
                <span className="mgc-val">{advisories.length}</span>
                <span className="mgc-label">Official Advisories</span>
              </div>
              <div className="metric-glass-card card active-mesh">
                <span className="mgc-val pulse-text">SYNCED</span>
                <span className="mgc-label">Telemetry Status</span>
              </div>
            </div>
          </motion.div>
        </div>
      </header>

      <div className="community-body container-narrow">
        <motion.section
          className="composer-section"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
        >
          <div className="composer-card card">
            <div className="composer-header-row"><span className="composer-icon">[Post]</span><h2 className="composer-title">Share a Live Update</h2></div>
            <textarea className="composer-textarea" placeholder="What are you seeing right now?" value={newText} onChange={(e) => setNewText(e.target.value)} rows={3} maxLength={280} />
            <div className="composer-meta-row">
              <input className="composer-input" type="text" placeholder="Your name" value={authorName} onChange={(e) => setAuthorName(e.target.value)} />
              <input className="composer-input" type="text" placeholder="Stand / Gate location" value={standLocation} onChange={(e) => setStandLocation(e.target.value)} />
              <select className="composer-select" value={postType} onChange={(e) => setPostType(e.target.value)}>
                <option value="crowd_report">Crowd Report</option>
                <option value="gate_update">Gate Update</option>
                <option value="food_tip">Food Tip</option>
                <option value="safety">Safety</option>
                <option value="general">General</option>
              </select>
            </div>
            <div className="composer-actions">
              <span className="char-count">{newText.length}/280</span>
              <button className="btn-primary" onClick={handleSubmit} disabled={submitting || !newText.trim()}>{submitting ? 'Posting...' : 'Post Live Update'}</button>
            </div>
            {showSuccess && <div className="success-toast"><span>[OK]</span> Your update is live.</div>}
          </div>
        </motion.section>

        <section className="feed-section" ref={feedRef}>
          <div className="feed-header-row"><h2 className="section-title">Live Feed</h2><span className="feed-live-badge"><span className="live-dot"></span>LIVE</span></div>
          <motion.div
            className="feed-list"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: '-80px' }}
          >
            {feedItems.length === 0 && <div className="empty-feed"><span className="empty-icon">[Live]</span><p>No posts yet. Be the first to share a live update.</p></div>}
            {feedItems.map((item) => {
              if (item._kind === 'advisory') {
                const adv = item as Advisory & { _kind: 'advisory' }
                return (
                  <motion.article variants={itemVariants} key={adv.id} className={`feed-card card advisory-card ${adv.is_pinned ? 'pinned' : ''} severity-${adv.severity}`}>
                    <div className="advisory-stripe"></div>
                    <div className="feed-card-inner">
                      <div className="advisory-badge-row">
                        <span className="verified-badge">OFFICIAL</span>
                        {adv.is_pinned && <span className="pin-badge">PINNED</span>}
                        <span className={`severity-badge sev-${adv.severity}`}>{adv.severity.toUpperCase()}</span>
                      </div>
                      <p className="feed-text">{adv.text}</p>
                      <div className="feed-meta"><span className="feed-author">{adv.author_name}</span><span className="feed-time">{fmt(adv.timestamp)}</span></div>
                    </div>
                  </motion.article>
                )
              }

              const post = item as CommunityPost & { _kind: 'post' }
              return (
                <motion.article variants={itemVariants} key={post.id} className="feed-card card post-card">
                  <div className="feed-card-inner">
                    <div className="post-top-row">
                      <span className="type-badge">{TYPE_ICONS[post.type] || '[Info]'} {TYPE_LABELS[post.type] || 'GENERAL'}</span>
                      <span className="helpful-badge">Helpful {post.helpful_count}</span>
                    </div>
                    <p className="feed-text">{post.text}</p>
                    <div className="feed-meta">
                      <span className="feed-author">{post.author_name}</span>
                      {post.stand_location && <span className="feed-location">At {post.stand_location}</span>}
                      <span className="feed-time">{fmt(post.timestamp)}</span>
                    </div>
                  </div>
                </motion.article>
              )
            })}
          </motion.div>
        </section>
      </div>
    </div>
  )
}
