import React from "react";

function Report({ criteria, report }) {
  return (
    <div style={{ marginTop: 24 }}>
      <h3>Relatório Detalhado</h3>
      {criteria && (
        <ul>
          {criteria.map((c) => (
            <li key={c.name}>
              <b>{c.name}</b>: {c.score} <br />
              <i>Justificativa:</i> {c.justification}
            </li>
          ))}
        </ul>
      )}
      {report && (
        <details style={{ marginTop: 16 }}>
          <summary>Relatório em Markdown</summary>
          <pre>{report}</pre>
        </details>
      )}
    </div>
  );
}

export default Report;
