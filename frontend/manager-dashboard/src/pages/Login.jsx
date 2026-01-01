// import { useNavigate } from "react-router-dom";

// export default function Login() {
//   const navigate = useNavigate();


// }

import { useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"


export default function Login() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const navigate = useNavigate()


  const handleLogin = async () => {
    try {
      const res = await axios.get("http://localhost:8000/manager/login", {
        params: {
          email: email,
          password: password
        }
      })

      sessionStorage.setItem("access_token", res.data.token)
      navigate("/dashboard")
    } catch (err) {
      alert(`Login failed ${err}`)
    }
  }

   return (
    <div className="h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded shadow w-80">
        <h2 className="text-xl font-bold mb-4">Login</h2>
                  <input
        placeholder="Mail id"
        onChange={e => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        onChange={e => setPassword(e.target.value)}
      />
        <button 
          onClick={handleLogin}
           className="w-full bg-blue-600 text-white py-2 rounded"
        >
          Login (Temporary)
        </button>
      </div>
    </div>
  );
}