import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { Workbench } from "./components/Workbench";

const queryClient = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Workbench />
    </QueryClientProvider>
  );
}
