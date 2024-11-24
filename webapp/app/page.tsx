import ProjectsPage from "./projects/page";
import LoginPage from "./login/page";

export default function Home() {
  const loggedIn = false;

  if (!loggedIn) {
    return <LoginPage />;
  }

  return <ProjectsPage />;
}
