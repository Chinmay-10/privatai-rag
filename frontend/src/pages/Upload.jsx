import Layout from "../components/Layout";
import api from "../api";

export default function Upload() {
  const upload = async (e) => {
    const file = e.target.files[0];
    const form = new FormData();
    form.append("file", file);
    await api.post("/upload/", form);
    alert("Document uploaded successfully");
  };

  return (
    <Layout title="Upload Document">
      <div className="bg-white border rounded-lg p-6 w-full max-w-xl">
        <input type="file" onChange={upload} />
      </div>
    </Layout>
  );
}
