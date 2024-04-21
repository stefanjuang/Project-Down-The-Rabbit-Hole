import { useEffect, useState } from "react";

async function fetchTweets(topic) {
  const response = await fetch(
    "http://127.0.0.1:8000/fetch_tweets_from_topic",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ topic }),
    }
  );

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  return response.json();
}

const Sidebar = ({ node }) => {
  const [tweets, setTweets] = useState([]);
  const [responseText, setResponseText] = useState("");
  //   const { complete } = useCompletion({
  //     api: "http://127.0.0.1:8000/analyze_topic",
  //   });

  useEffect(() => {
    if (node) {
      fetchTweets(node.id).then(setTweets).catch(console.error);
    }
  }, [node]);

  useEffect(() => {
    const fetchData = async () => {
      if (!node) return;

      const body = {
        user: "Elon Musk",
        topic: node.id,
      };
      const response = await fetch("http://127.0.0.1:8000/analyze_topic", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!response.body) {
        console.error("Failed to get readable stream");
        return;
      }

      const reader = response.body.getReader();
      let chunks = "";

      const readChunk = async ({ done, value }) => {
        if (done) {
          console.log("Stream finished.");
          return;
        }

        const strVal = new TextDecoder().decode(value);
        chunks += strVal;
        // Update the state with the new chunk appended
        setResponseText((prevText) => prevText + strVal);

        // Read the next chunk
        return reader.read().then(readChunk);
      };

      reader
        .read()
        .then(readChunk)
        .catch((error) => {
          console.error("Error reading the stream", error);
        });
    };

    fetchData();
  }, [node]);

  //   useEffect(() => {
  //     const fetchInsights = async () => {
  //       try {
  //         const insightsResult = complete("", {
  //           body: {
  //             user: "Elon Musk",
  //             topic: node.id,
  //           },
  //         });
  //         console.log(insightsResult);
  //       } catch (error) {
  //         console.error("Failed to fetch insights:", error);
  //       }
  //     };
  //     fetchInsights();
  //   }, [tweets, node.id]);

  const renderInsightWithLinks = (insight) => {
    const regex = /\[\$(\d+)\]/g; // Matches [$`index`]
    return (
      <p
        dangerouslySetInnerHTML={{
          __html: insight.summary.replace(regex, (match, index) => {
            const tweet = tweets.find((t) => t.index === parseInt(index));
            return tweet
              ? `<a href="${tweet.url}" target="_blank" rel="noopener noreferrer">${match}</a>`
              : match;
          }),
        }}
      />
    );
  };

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
      <h2>Node Details</h2>
      <p>ID: {node.id}</p>
      <p>Group: {node.group}</p>
      <div style={{ display: "flex", overflowX: "auto" }}>
        {tweets.map((tweet) => (
          <div key={tweet.index} style={{ marginRight: "20px" }}>
            <p>{tweet.text}</p>
          </div>
        ))}
      </div>
      <div>
        {responseText}
        {/* {insights.map((insight, index) => (
          <div key={index}>{renderInsightWithLinks(insight)}</div>
        ))} */}
      </div>
    </div>
  );
};

export default Sidebar;
