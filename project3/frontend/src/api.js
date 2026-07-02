const BASE_URL = "http://localhost:8000";

export async function getTable(tableId) {
  const res = await fetch(`${BASE_URL}/table/${tableId}`);
  return res.json();
}

export async function addRandomRow(tableId) {
  const res = await fetch(`${BASE_URL}/add/${tableId}`, {
    method: "POST",
  });
  return res.json();
}

export async function deleteRandomRow(tableId) {
  const res = await fetch(`${BASE_URL}/delete/${tableId}`, {
    method: "DELETE",
  });
  return res.json();
}