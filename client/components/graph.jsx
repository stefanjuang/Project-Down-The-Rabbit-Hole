"use client";

import data from "@/datasets/data.json";
import { useCallback, useRef, useState } from "react";
import ForceGraph3D from "react-force-graph-3d";
import SpriteText from "three-spritetext";
import SideBar from "./side-bar";

const Graph = () => {
  const fgRef = useRef();
  const [selectedNode, setSelectedNode] = useState(null);

  const handleClick = useCallback(
    (node) => {
      setSelectedNode(node);
    },
    [fgRef]
  );

  return (
    <div className="flex flex-1">
      <ForceGraph3D
        ref={fgRef}
        graphData={data}
        nodeAutoColorBy="group"
        nodeThreeObject={(node) => {
          const sprite = new SpriteText(node.id);
          sprite.color = node.color;
          sprite.textHeight = 8;
          return sprite;
        }}
        onNodeClick={handleClick}
      />
      {selectedNode && <SideBar node={selectedNode} />}
    </div>
  );
};

export default Graph;
