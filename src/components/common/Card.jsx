export default function Card({ title, children, className = '' }) {
  return <div className={`card ${className}`}>{title ? <h3>{title}</h3> : null}{children}</div>
}
