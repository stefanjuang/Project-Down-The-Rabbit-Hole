import { Graph } from "@/components/graph-no-ssr";
import SearchInput from "@/components/search";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between">
      <SearchInput />
      <Graph />
    </main>
  );
}
