// src/components/__tests__/Header.test.tsx
import { render, screen } from "@testing-library/react";
import { Header } from "../Header";

describe("Header", () => {
  it("renders the logo and title", () => {
    render(<Header />);

    expect(screen.getByText("La Vida Luca")).toBeInTheDocument();
    expect(screen.getByText("VL")).toBeInTheDocument();
  });

  it("renders navigation links", () => {
    render(<Header />);

    expect(screen.getByText("Notre mission")).toBeInTheDocument();
    expect(screen.getByText("Activités")).toBeInTheDocument();
    expect(screen.getByText("Contact")).toBeInTheDocument();
  });
});
