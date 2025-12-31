import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  return (
    <div className="h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded shadow w-80">
        <h2 className="text-xl font-bold mb-4">Login</h2>

        <button
          onClick={() => navigate("/dashboard")}
          className="w-full bg-blue-600 text-white py-2 rounded"
        >
          Login (Temporary)
        </button>
      </div>
    </div>
  );
}
