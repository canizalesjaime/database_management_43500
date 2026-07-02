import { useState, useEffect } from "react";
import { getTable, addRandomRow, deleteRandomRow } from "./api";
import "./styles.css";

//const TABLES = ["table1", "table2", "table3", "table4", "table5"];
const TABLES = ["employees", "salaries", "titles", "departments", "dept_emp"];
export default function App() {
  const [activeTable, setActiveTable] = useState(TABLES[0]);
  const [rows, setRows] = useState([]);

  async function loadTable(tableId) {
    const data = await getTable(tableId);
    setRows(data.rows || []);
  }

  useEffect(() => {
    loadTable(activeTable);
  }, [activeTable]);

  async function handleAdd() {
    await addRandomRow(activeTable);
    loadTable(activeTable);
  }

  async function handleDelete() {
    await deleteRandomRow(activeTable);
    loadTable(activeTable);
  }

  return (
    <div className="container">
      <h1>Database Viewer</h1>

      {/* Tabs */}
      <div className="tabs">
        {TABLES.map((t) => (
          <button
            key={t}
            className={t === activeTable ? "active" : ""}
            onClick={() => setActiveTable(t)}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Actions */}
      <div className="actions">
        <button onClick={handleAdd}>Add Random Row</button>
        <button onClick={handleDelete}>Delete Random Row</button>
      </div>

      {/* Table Display */}
      <table>
        <thead>
          <tr>
            {rows[0] &&
              Object.keys(rows[0]).map((col) => (
                <th key={col}>{col}</th>
              ))}
          </tr>
        </thead>

        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {Object.values(row).map((val, j) => (
                <td key={j}>{val}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}