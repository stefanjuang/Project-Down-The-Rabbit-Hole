const Sidebar = ({ node }) => {
  if (!node) return null;
  return (
    <div
      style={{
        width: "700px",
        flexShrink: 0,
        height: "100vh",
        overflow: "auto",
      }}
    >
      {/* Render selected node details here */}
      <h2>Node Details</h2>
      <p>ID: {node.id}</p>
      <p>Group: {node.group}</p>
      {/* Add more node details as needed */}
    </div>
  );
};

export default Sidebar;
