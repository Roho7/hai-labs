import { Activity } from "react-feather";
import { ChatBox } from "./components/ChatBox";

export default function Home() {
  return (
    <main className="flex flex-col gap-2 items-center justify-between p-24">
      <h1 className="text-2xl font-bold flex gap-2 p-4 bg-slate-800 rounded-md">
        <Activity />
        Zeitkönig
      </h1>
      <ChatBox />
    </main>
  );
}
