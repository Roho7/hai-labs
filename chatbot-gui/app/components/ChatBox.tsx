"use client";
import axios from "axios";
import { useEffect, useState } from "react";
import { Response } from "./Response";
import { Send } from "react-feather";

interface ResponseType {
  data: string;
}

export const ChatBox = () => {
  const [chat, setChat] = useState<string>();
  const [placeholder, setPlaceholder] = useState("'Add cooking at 7pm'");
  const [response, setResponse] = useState<ResponseType>({ data: "" });
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setChat(e.target.value);
  };
  const getData = async (e: React.FormEvent) => {
    e.preventDefault();
    const msg = { msg: chat };
    try {
      const data = await axios.post("http://127.0.0.1:5000/chat", msg);
      setChat("");
      setResponse(data);
    } catch (err) {
      console.log(err);
    }
  };

  const placeholdersArr = [
    "'Add cooking at 7pm' ",
    "'What can you do?'",
    "'What's up?'",
    "'What is the weather like today?'",
    "'What does my day look like?'",
    "'Who are you?'",
    "'How's it hanging?'",
    "'Tell me a joke'",
    "'Who built you?'",
    "'Show me my schedule'",
  ];
  useEffect(() => {
    const interval = setInterval(() => {
      const rand = Math.floor(Math.random() * 9);
      setPlaceholder(placeholdersArr[rand]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);
  return (
    <div className="flex flex-col gap-2 w-full">
      <div>
        <Response msg={response.data} />
      </div>

      <form action="" onSubmit={getData} className="flex gap-2">
        <input
          type="text"
          className="text-black p-4 rounded-md bg-slate-200 w-full"
          onChange={handleChange}
          value={chat}
          placeholder={placeholder}
        />
        <button type="submit" className=" bg-yellow-600 p-4 rounded-md">
          <Send />
        </button>
      </form>
    </div>
  );
};
