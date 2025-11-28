import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabaseClient";

export default function FeedbackPanel({ selectedSpot = null, clientSessionId = null }) {
  const [open, setOpen] = useState(() => {
    try {
      return localStorage.getItem("feedback_panel_open") !== "false";
    } catch {
      return true;
    }
  });

  const [busy, setBusy] = useState(5);
  const [accuracy, setAccuracy] = useState(5);
  const [comment, setComment] = useState("");
  const [status, setStatus] = useState("idle");
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    localStorage.setItem("feedback_panel_open", open ? "true" : "false");
  }, [open]);

  const submit = async () => {
    if (status === "sending") return;
    setStatus("sending");
    setErrorMsg("");

    const payload = {
      spot_id: selectedSpot ? selectedSpot.id : null,
      busy_rating: busy,
      accuracy_rating: accuracy,
      comment: comment || null,
      client_session_id: clientSessionId,
    };

    const { error } = await supabase.from("feedback").insert([payload]);
    if (error) {
      setErrorMsg(error.message);
      setStatus("error");
      return;
    }

    setStatus("success");
    setTimeout(() => {
      setStatus("idle");
      setBusy(5);
      setAccuracy(5);
      setComment("");
    }, 1600);
  };

  const panelStyle = {
    position: "fixed",
    right: "20px",
    bottom: "20px",
    width: "340px",
    maxWidth: "calc(100% - 40px)",
    background: "#161617",
    color: "#fff",
    boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
    borderRadius: "12px",
    zIndex: 9999,
    transform: open ? "translateY(0)" : "translateY(92%)",  // ⭐ FIX
    transition: "transform 330ms cubic-bezier(.2,.8,.2,1), opacity 300ms",
    opacity: open ? 1 : 0.95,
    overflow: "hidden",
  };

  return (
    <div style={panelStyle}>
      <div
        style={{
          padding: "10px 14px",
          display: "flex",
          justifyContent: "space-between",
          background: "#19191a",
        }}
      >
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <button
            onClick={() => setOpen((o) => !o)}
            style={{
              width: 36,
              height: 36,
              borderRadius: 8,
              border: "none",
              background: "transparent",
              color: "white",
              cursor: "pointer",
              fontSize: 18,
            }}
          >
            {open ? "✕" : "✉️"}
          </button>
          <div>
            <div style={{ fontWeight: 700 }}>Feedback</div>
            <div style={{ fontSize: 12, opacity: 0.7 }}>
              {selectedSpot ? selectedSpot.name : "Tell us about this spot"}
            </div>
          </div>
        </div>
      </div>

      <div style={{ padding: "12px 14px" }}>
        {/* Busy slider */}
        <label style={{ display: "block", marginBottom: 6 }}>
          How busy was it? <strong>{busy}</strong>
        </label>
        <input type="range" min="1" max="10" value={busy}
               onChange={(e) => setBusy(Number(e.target.value))}
               style={{ width: "100%" }} />

        <div style={{ height: 14 }} />

        {/* Accuracy slider */}
        <label style={{ display: "block", marginBottom: 6 }}>
          Was the description accurate? <strong>{accuracy}</strong>
        </label>
        <input type="range" min="1" max="10" value={accuracy}
               onChange={(e) => setAccuracy(Number(e.target.value))}
               style={{ width: "100%" }} />

        <div style={{ height: 14 }} />

        {/* Comment */}
        <label style={{ display: "block", marginBottom: 6 }}>
          Comments (optional)
        </label>
        <textarea
          placeholder="Short note about the spot..."
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          style={{
            width: "100%",
            minHeight: 80,
            padding: 10,
            borderRadius: 8,
            background: "#0f0f10",
            color: "white",
            border: "1px solid rgba(255,255,255,0.1)",
            resize: "vertical",
          }}
        />

        <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
          <button
            onClick={submit}
            disabled={status === "sending"}
            style={{
              flex: 1,
              background: "#3b82f6",
              padding: "10px",
              borderRadius: 8,
              border: "none",
              color: "white",
              cursor: "pointer",
            }}
          >
            {status === "sending" ? "Sending..." : "Submit"}
          </button>

          <button
            onClick={() => {
              setBusy(5);
              setAccuracy(5);
              setComment("");
            }}
            style={{
              padding: "10px",
              borderRadius: 8,
              border: "1px solid rgba(255,255,255,0.2)",
              background: "transparent",
              color: "white",
            }}
          >
            Reset
          </button>
        </div>

        {status === "success" && (
          <div style={{
            marginTop: 12,
            padding: 12,
            background: "#2fa360",
            borderRadius: 8,
            textAlign: "center",
          }}>
            Thanks — feedback submitted!
          </div>
        )}

        {status === "error" && (
          <div style={{
            marginTop: 12,
            padding: 12,
            background: "#b71c1c",
            borderRadius: 8,
            textAlign: "center",
          }}>
            Error: {errorMsg}
          </div>
        )}
      </div>
    </div>
  );
}
