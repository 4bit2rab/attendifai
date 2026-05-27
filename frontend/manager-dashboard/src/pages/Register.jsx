// import { useState } from "react";
// import { registerUser } from "../api/authApi";
// import { useNavigate } from "react-router-dom";

// export default function Register() {
//   const navigate = useNavigate();
//   const [form, setForm] = useState({
//     name: "",
//     email: "",
//     password: "",
//   });

//   const [loading, setLoading] = useState(false);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setLoading(true);

//     try {
//       await registerUser(form);
//       alert("Registration successful!");
//       navigate("/");
//     } catch {
//       alert("Registration failed");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-gray-100">
//       <div className="bg-white p-6 rounded shadow w-96">
//         <h2 className="text-xl font-bold mb-4">Register</h2>

//         <form onSubmit={handleSubmit} className="space-y-3">
//           <input
//             type="text"
//             placeholder="Name"
//             className="w-full border p-2 rounded"
//             value={form.name}
//             onChange={(e) => setForm({ ...form, name: e.target.value })}
//             required
//           />

//           <input
//             type="email"
//             placeholder="Email"
//             className="w-full border p-2 rounded"
//             value={form.email}
//             onChange={(e) => setForm({ ...form, email: e.target.value })}
//             required
//           />

//           <input
//             type="password"
//             placeholder="Password"
//             className="w-full border p-2 rounded"
//             value={form.password}
//             onChange={(e) => setForm({ ...form, password: e.target.value })}
//             required
//           />

//           <button
//             type="submit"
//             className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
//           >
//             {loading ? "Creating..." : "Register"}
//           </button>
//         </form>
//       </div>
//     </div>
//   );
// }

import { useState } from "react"
import { registerUser } from "../api/authApi"
import { Link } from "react-router-dom"

export default function Register() {

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: ""
  })

  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState("")

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  const validate = () => {
    const newErrors = {}

    if (!form.name.trim()) {
      newErrors.name = "Name is required"
    }

    if (!form.email.trim()) {
      newErrors.email = "Email is required"
    } else if (!emailRegex.test(form.email)) {
      newErrors.email = "Enter a valid email address"
    }

    if (!form.password.trim()) {
      newErrors.password = "Password is required"
    } else if (form.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters"
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSuccess("")

    if (!validate()) return

    setLoading(true)

    try {
      await registerUser(form)
      setSuccess("Registration successful!!")
      setForm({ name: "", email: "", password: "" }) 
        setTimeout(() => {
          setSuccess("")
        }, 1500) 

    } catch {
      setErrors({ form: "Registration failed. Try again." })
      setForm({
        name: "",
        email: "",
        password: ""
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">

        {/* Success message */}
        {success && (
          <div className="mb-3 text-green-700 bg-green-100 border border-green-300 rounded p-2 text-sm text-center">
            {success}
          </div>
        )}

        {/* Header */}
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">
            Create Manager Account
          </h2>
          <p className="text-sm text-gray-500">
            Register to manage employees
          </p>
        </div>

        {/* FORM ERROR */}
        {errors.form && (
          <p className="text-red-600 text-sm mb-4 text-center">
            {errors.form}
          </p>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">

          {/* Name */}
          <div>
            <input
              type="text"
              placeholder="Full Name"
              className={`w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring-2
                ${errors.name ? "border-red-500 focus:ring-red-400" : "focus:ring-green-500"}`}
              value={form.name}
              onChange={e =>
                setForm({ ...form, name: e.target.value })
              }
              required
            />
            {errors.name && (
              <p className="text-red-500 text-xs mt-1">
                {errors.name}
              </p>
            )}
          </div>

          {/* Email */}
          <div>
            <input
              type="email"
              placeholder="Email address"
              className={`w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring-2
                ${errors.email ? "border-red-500 focus:ring-red-400" : "focus:ring-green-500"}`}
              value={form.email}
              onChange={e =>
                setForm({ ...form, email: e.target.value })
              }
              required
            />
            {errors.email && (
              <p className="text-red-500 text-xs mt-1">
                {errors.email}
              </p>
            )}
          </div>

          {/* Password */}
          <div>
            <input
              type="password"
              placeholder="Password"
              className={`w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring-2
                ${errors.password ? "border-red-500 focus:ring-red-400" : "focus:ring-green-500"}`}
              value={form.password}
              onChange={e =>
                setForm({ ...form, password: e.target.value })
              }
              required
            />
            {errors.password && (
              <p className="text-red-500 text-xs mt-1">
                {errors.password}
              </p>
            )}
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 text-white py-2 rounded-lg font-medium hover:bg-green-700 transition disabled:opacity-50"
          >
            {loading ? "Creating..." : "Register"}
          </button>
        </form>

        {/* Login Link */}
        <p className="text-center text-sm text-gray-600 mt-4">
          Already have an account?{" "}
          <Link
            to="/"
            className="text-green-600 hover:underline font-medium"
          >
            Login
          </Link>
        </p>

      </div>
    </div>
  )
}
