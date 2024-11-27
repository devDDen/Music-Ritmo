import Image from "next/image";
import Logo from "../../public/images/logo.svg";

import { Button } from "@/shared/button";

export default function Home() {
  return (
    <div>
      <h1>Добро пожаловать в musicRitmo!</h1>
      <h2>Добро пожаловать в musicRitmo!</h2>
      <p>Добро пожаловать в musicRitmo!</p>
      <Image src={Logo} alt="Логотип musicRitmo" width={100} height={100} />
      <i className="fa-regular fa-heart"></i>
      <Button type="normal" color="green" disabled={true}>
        вход
      </Button>
      <Button type="normal" color="white" disabled={true}>
        вход
      </Button>
      <Button type="transparent" color="green-text">
        вход
      </Button>
    </div>
  );
}
