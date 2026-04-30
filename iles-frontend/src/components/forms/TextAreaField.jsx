export default function TextAreaField({ label, ...props }) {
  return <label className="field"><span>{label}</span><textarea {...props} /></label>
}
