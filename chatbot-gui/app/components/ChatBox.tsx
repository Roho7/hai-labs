"use client";
import axios from "axios";
import { useState } from "react";
import { Response } from "./Response";
import { Send } from "react-feather";

interface ResponseType {
  data: string;
}

export const ChatBox = () => {
  const [chat, setChat] = useState<string>();
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
        />
        <button type="submit" className="bg-gray-500 p-4 rounded-md">
          <Send />
        </button>
      </form>
    </div>
  );
};
