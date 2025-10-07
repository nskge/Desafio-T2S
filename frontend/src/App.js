import React, { useState } from "react";
import axios from "axios";
import Ranking from "./components/Ranking";
import Report from "./components/Report";

function App() {
  const [urls, setUrls] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/submit", {
        urls: urls.split(/\s|,/).filter((u) => u)
      });
      setResults(response.data);
    } catch (err) {
      alert("Erro ao submeter URLs");
    }
    setLoading(false);
  };

  const handleSelect = async (repo_url) => {
    try {
      const response = await axios.get(`http://localhost:8000/report/${repo_url}`);
      setSelected(response.data);
    } catch {
      setSelected(null);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "auto", padding: 32 }}>
      <h1>T2S Hackathon - Avaliação de Projetos</h1>
      <form onSubmit={handleSubmit}>
        <label>URLs dos repositórios (separadas por espaço ou vírgula):</label>
        <textarea
          value={urls}
          onChange={(e) => setUrls(e.target.value)}
          rows={4}
          style={{ width: "100%" }}
        />
        <button type="submit" disabled={loading} style={{ marginTop: 16 }}>
          {loading ? "Analisando..." : "Submeter"}
        </button>
      </form>
      <Ranking />
      <h2 style={{ marginTop: 32 }}>Resultados</h2>
      <ul>
        {results.map((r) => (
          <li key={r.repo_url}>
            <b>{r.repo_url}</b>: {r.status}
            {r.total_score && <span> | Pontuação: {r.total_score}</span>}
            <button style={{ marginLeft: 8 }} onClick={() => handleSelect(r.repo_url)}>
              Ver relatório
            </button>
          </li>
        ))}
      </ul>
      {selected && <Report criteria={selected.criteria} report={selected.report} />}
    </div>
  );
}

export default App;
