export async function uploadContract(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:8000/upload", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Upload failed");
  }

  return await response.json();
}
