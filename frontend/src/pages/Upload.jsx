import FileUpload from "../components/FileUpload";

export default function Upload() {
  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Upload Your Contract</h1>
      <p className="mb-6 text-gray-600">
        We’ll analyze this contract to extract key clauses and detect risks.
      </p>
      <FileUpload />
    </div>
  );
}
