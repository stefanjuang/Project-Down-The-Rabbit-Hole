import { useEffect, useState } from "react";
import { Tweet } from "react-tweet";
import { Badge } from "./ui/badge";

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

      // Function to handle the stream processing
      const processStream = async () => {
        let chunks = "";
        let receivedLength = 0; // to count binary data length
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            console.log("Stream finished.");
            break;
          }
          chunks += new TextDecoder().decode(value);
          receivedLength += value.length;

          // For example, you could update the state every N bytes
          if (receivedLength > 64) {
            // Arbitrary threshold
            setResponseText((prevText) => prevText + chunks);
            chunks = "";
            receivedLength = 0;
          }
        }

        // Ensure any remaining data is set
        if (chunks.length > 0) {
          setResponseText((prevText) => prevText + chunks);
        }
      };

      processStream().catch((error) => {
        console.error("Error reading the stream", error);
      });
    };

    fetchData();
  }, [node]);

  const renderInsightWithLinks = (insight) => {
    const regex = /\[(\d+)\]/g;
    const parts = insight.split(regex);

    return (
      <p>
        {parts.map((part, index) => {
          if (index % 2 === 0) {
            // Render Markdown for non-link parts
            return part;
          } else {
            const tweetIndex = parseInt(part, 10);
            const tweet = tweets.find((t) => t.index === tweetIndex);
            if (tweet) {
              return (
                <a href={tweet.url} target="_blank" rel="noopener noreferrer">
                  <Badge variant="secondary">{tweetIndex}</Badge>
                </a>
              );
            } else {
              return `[${part}]`;
            }
          }
        })}
      </p>
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
      <div className="flex overflow-x-auto gap-4">
        {tweets.map((tweet) => {
          const tweetId = tweet.url.split("/").pop(); // Extracts the ID from the URL
          return (
            <div
              className="flex flex-col items-center w-128 h-128 shadow-md rounded-lg"
              key={tweet.index}
            >
              <Badge variant="secondary">{tweet.index}</Badge>
              <Tweet id={tweetId} />
            </div>
          );
        })}
      </div>
      <div>{renderInsightWithLinks(responseText)}</div>
    </div>
  );
};

export default Sidebar;
