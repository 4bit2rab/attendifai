export const logout = (navigate) => {
  sessionStorage.clear()

  navigate("/", { replace: true });
}
