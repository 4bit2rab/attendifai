import { BellIcon, UserCircleIcon } from "lucide-react";

export default function Topbar() {
  return (
    <div className="bg-white shadow flex items-center justify-between px-6 py-3 sticky top-0 z-50">
      {/* Left: App Name */}
      <h1 className="text-xl font-bold text-gray-800">Attendifai</h1>

      {/* Right: Notifications + Profile */}
      <div className="flex items-center space-x-4">
        <button className="relative p-2 rounded-full hover:bg-gray-100 transition-colors duration-200">
          <BellIcon className="w-6 h-6 text-gray-600" />
          <span className="absolute top-0 right-0 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white bg-red-500 rounded-full">
            3
          </span>
        </button>

        <div className="flex items-center space-x-2 cursor-pointer hover:bg-gray-100 rounded-full p-1 transition-all duration-200">
          <UserCircleIcon className="w-8 h-8 text-gray-600" />
          <span className="text-gray-800 font-medium">Manager Name</span>
        </div>
      </div>
    </div>
  );
}
