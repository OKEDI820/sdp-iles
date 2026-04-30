export default function InputField({ label, ...props }) {
  return <label className="field"><span>{label}</span><input {...props} /></label>
}
