// import { useState } from "react"
// import axios from "axios"
// import { useNavigate, Link } from "react-router-dom"

// export default function Login() {
//   const [email, setEmail] = useState("")
//   const [password, setPassword] = useState("")
//   const [loading, setLoading] = useState(false)
//   const [error, setError] = useState("")
//   const navigate = useNavigate()

//   const handleLogin = async () => {
//     setError("")
//     setLoading(true)

//     try {
//       const res = await axios.get("http://localhost:8000/manager/login", {
//         params: { email, password }
//       })

//       sessionStorage.setItem("access_token", res.data.token)
//       navigate("/dashboard", { replace: true })
//     } catch (err) {
//       setError(`Invalid email or password`)
//       console.error("Login failed:", err)
//     } finally {
//       setLoading(false)
//     }
//   }

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100">
//       <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-sm">
        
//         {/* Header */}
//         <div className="text-center mb-6">
//           <h2 className="text-2xl font-bold text-gray-800">Manager Login</h2>
//         </div>

//         {/* Email */}
//         <div className="mb-4">
//           <label className="block text-sm text-gray-600 mb-1">
//             Email address
//           </label>
//           <input
//             type="email"
//             required
//             placeholder="manager@company.com"
//             value={email}
//             onChange={e => setEmail(e.target.value)}
//             className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
//           />
//         </div>

//         {/* Password */}
//         <div className="mb-4">
//           <label className="block text-sm text-gray-600 mb-1">
//             Password
//           </label>
//           <input
//             type="password"
//             required
//             placeholder="••••••••"
//             value={password}
//             onChange={e => setPassword(e.target.value)}
//             className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
//           />
//         </div>

//         {/* Error */}
//         {error && (
//           <p className="text-sm text-red-600 mb-3 text-center">
//             {error}
//           </p>
//         )}

//         {/* Login Button */}
//         <button
//           onClick={handleLogin}
//           disabled={loading}
//           className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium transition disabled:opacity-50"
//         >
//           {loading ? "Signing in..." : "Login"}
//         </button>

//         {/* Create Account */}
//         <p className="text-center text-sm text-gray-600 mt-4">
//           Don’t have an account?{" "}
//           <Link
//             to="/register"
//             className="text-blue-600 hover:underline font-medium"
//           >
//             Create new
//           </Link>
//         </p>
//       </div>
//     </div>
//   )
// }


import { useState } from "react"
import axios from "axios"
import { useNavigate, Link } from "react-router-dom"

export default function Login() {
  const navigate = useNavigate()

  const [form, setForm] = useState({
    email: "",
    password: "",
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      const res = await axios.get("http://localhost:8000/manager/login", {
        params: form,
      })

      sessionStorage.setItem("access_token", res.data.token)
      navigate("/dashboard", { replace: true })
    } catch {
      setError("Invalid email or password")
      setForm({ email: "", password: "" })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100">
      <div className="bg-white p-8 rounded-xl shadow-lg w-96">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
          Manager Login
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Email */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Email
            </label>
            <input
              type="email"
              required
              placeholder="manager@company.com"
              value={form.email}
              onChange={(e) =>
                setForm({ ...form, email: e.target.value })
              }
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              Password
            </label>
            <input
              type="password"
              required
              placeholder="••••••••"
              value={form.password}
              onChange={(e) =>
                setForm({ ...form, password: e.target.value })
              }
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Error */}
          {error && (
            <p className="text-sm text-red-600 text-center">
              {error}
            </p>
          )}

          {/* Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium transition disabled:opacity-50"
          >
            {loading ? "Signing in..." : "Login"}
          </button>
        </form>

        {/* Register */}
        <p className="text-center text-sm text-gray-600 mt-5">
          Don’t have an account?{" "}
          <Link
            to="/register"
            className="text-blue-600 hover:underline font-medium"
          >
            Create new
          </Link>
        </p>
      </div>
    </div>
  )
}
