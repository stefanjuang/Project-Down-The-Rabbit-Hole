import dynamic from "next/dynamic";

export const Graph = dynamic(() => import("./graph"), {
  ssr: false,
});
