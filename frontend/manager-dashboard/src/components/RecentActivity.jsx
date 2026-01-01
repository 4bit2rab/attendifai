const activities = [
  { name: "John Doe", status: "Checked in", time: "09:02 AM" },
  { name: "Sarah Smith", status: "Late check-in", time: "09:18 AM" },
  { name: "Michael Lee", status: "Absent", time: "-" },
  { name: "Priya Nair", status: "Checked in", time: "08:56 AM" },
];

export default function RecentActivity() {
  return (
    <ul className="space-y-4">
      {activities.map((item, index) => (
        <li key={index} className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-900">
              {item.name}
            </p>
            <p className="text-xs text-gray-500">
              {item.status}
            </p>
          </div>
          <span className="text-xs text-gray-400">
            {item.time}
          </span>
        </li>
      ))}
    </ul>
  );
}
