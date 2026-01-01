import { BellIcon, UserCircleIcon } from "lucide-react";

export default function Topbar() {
  return (
    <header className="bg-white border-b px-6 py-4 flex items-center justify-between sticky top-0 z-40">
      {/* Page Title */}
      <h1 className="text-lg font-semibold text-gray-800">
        Hi there!
      </h1>

      {/* Right actions */}
      <div className="flex items-center gap-4">
        {/* Notification */}
        <button className="relative p-2 rounded-full hover:bg-gray-100 transition">
          <BellIcon className="w-6 h-6 text-gray-600" />
          <span className="absolute -top-1 -right-1 w-5 h-5 text-xs flex items-center justify-center bg-red-500 text-white rounded-full">
            3
          </span>
        </button>

        {/* Profile */}
        <div className="flex items-center gap-2 cursor-pointer hover:bg-gray-100 px-3 py-1.5 rounded-full transition">
          <UserCircleIcon className="w-8 h-8 text-gray-600" />
          <span className="text-gray-800 font-medium hidden sm:block">
            Manager
          </span>
        </div>
      </div>
    </header>
  );
}
