import { useState } from "react";
import axios from "axios";

export default function DataUpload() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload", formData);
      setData(response.data);
    } catch (error) {
      console.error("Dosya yüklenirken hata oluştu:", error);
    }
  };

  return (
    <div>
      <h2>CSV Dosyanızı Yükleyin</h2>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload}>Yükle</button>

      {data && (
        <div>
          <h3>İşlenmiş Veri:</h3>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

