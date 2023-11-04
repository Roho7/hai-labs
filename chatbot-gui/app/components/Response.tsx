interface PropsType {
  msg: string;
}
export const Response = ({ msg }: PropsType) => {
  const input = JSON.stringify(msg).replace(/["]/g, "");
  const data = input.charAt(0).toUpperCase() + input.slice(1);
  return (
    <div className="p-4 flex items-center justify-center bg-gray-700 rounded-md h-96">
      <div>{data}</div>
    </div>
  );
};
