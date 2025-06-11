import { useState } from "react";
import { uploadContract } from "../services/api";


export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle");

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    try {
      await uploadContract(file);
      setStatus("success");
    } catch (err) {
      setStatus("error");
    }
  };

  return (
    <div>
      <input
        className="mt-4 bg-blue-600 text-white mx-4 py-2 rounded"
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button
        onClick={handleUpload}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
      >
        Upload
      </button>
      {status === "uploading" && <p>Uploading...</p>}
      {status === "success" && <p className="text-green-600">Uploaded!</p>}
      {status === "error" && <p className="text-red-600">Failed to upload.</p>}
    </div>
  );
}
