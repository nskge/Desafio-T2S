import React, { useState, useEffect } from "react";
import axios from "axios";

function Ranking() {
  const [ranking, setRanking] = useState([]);
  useEffect(() => {
    axios.get("http://localhost:8000/ranking").then((res) => {
      setRanking(res.data);
    });
  }, []);
  return (
    <div>
      <h2>Ranking dos Projetos</h2>
      <ol>
        {ranking.map((r) => (
          <li key={r.repo_url}>
            <b>{r.repo_url}</b> — Pontuação: {r.total_score}
          </li>
        ))}
      </ol>
    </div>
  );
}

export default Ranking;
