const { register, login, logout } = (() => {
  class API {
    static _token = null;

    static async _fetch(endpoint, body) {
      const res = await fetch(`/api/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(API._token ? { Authorization: `Bearer ${API._token}` } : {}),
        },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const error = await res.json();
        alert(error.error);
        throw new Error(error.error);
      }
      return await res.json();
    }

    static set_token(token) {
      API._token = token;
    }

    static async register(username) {
      const data = API._fetch("register", { username });
      return data;
    }

    static async login(username, password) {
      const data = API._fetch("login", { username, password });
      return data;
    }

    static async admin() {
      const data = API._fetch("admin", {});
      return data;
    }
  }

  async function register(event) {
    event.preventDefault();

    const data = new FormData(event.target);

    const res = await API.register(data.get("username"));
    alert(`Your account has been created with password ${res.password}`);

    API.set_token(res.token);
    renderMenu(res.is_admin);
    renderHome(data.get("username"));
  }

  async function login(event) {
    event.preventDefault();

    const data = new FormData(event.target);

    const res = await API.login(data.get("username"), data.get("password"));
    API.set_token(res.token);
    renderMenu(res.is_admin);
    renderHome(data.get("username"));
  }

  function logout() {
    window.location.href = window.location.href;
  }

  function renderMenu(is_admin) {
    const menu = document.querySelector("#menu");
    while (menu.childElementCount > 0) {
      menu.removeChild(menu.lastChild);
    }

    if (is_admin) {
      const admin = document.createElement("li");
      const a = document.createElement("a");
      a.onclick = () => {
        const container = document.querySelector("#container");
        while (container.childElementCount > 0) {
          container.removeChild(container.lastChild);
        }

        const h1 = document.createElement("h1");
        h1.classList = "text-4xl font-bold text-center";
        h1.innerText = "Welcome to the admin panel";
        container.appendChild(h1);

        const center = document.createElement("div");
        center.classList = "text-center mt-16";
        container.appendChild(center);

        const button = document.createElement("button");
        button.classList =
          "bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 cursor-pointer";
        button.innerText = "Admin action";
        button.onclick = async () => {
          const res = await API.admin();
          alert(res.message);
        };
        center.appendChild(button);
      };
      a.classList = "cursor-pointer hover:underline";
      a.innerText = "Admin";
      admin.appendChild(a);
      menu.appendChild(admin);
    }

    const logoutBtn = document.createElement("li");
    const a = document.createElement("a");
    a.onclick = logout;
    a.classList = "cursor-pointer hover:underline";
    a.innerText = "Logout";
    logoutBtn.appendChild(a);
    menu.appendChild(logoutBtn);
  }

  function renderHome(username) {
    const container = document.querySelector("#container");
    while (container.childElementCount > 0) {
      container.removeChild(container.lastChild);
    }

    const h1 = document.createElement("h1");
    h1.classList = "text-4xl font-bold text-center";
    h1.innerText = "Welcome back!";
    container.appendChild(h1);

    const p = document.createElement("p");
    p.classList = "text-center mt-16";
    p.innerText = `Welcome back, ${username}`;
    container.appendChild(p);
  }

  return { register, login, logout };
})();
