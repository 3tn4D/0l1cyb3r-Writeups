import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Nav from 'react-bootstrap/Nav';
import Alert from 'react-bootstrap/Alert';
import Container from 'react-bootstrap/Container';
import { Switch, Route, Link, useHistory } from 'react-router-dom';
import Login from './Login.js';
import { useState, useEffect } from 'react';
import ModificaStile from './ModificaStile';

export default function Main(props) {
  let history = useHistory();

  const [auth, setAuth] = useState(false);
  const [hcaptchaSiteKey, setHcaptchaSiteKey] = useState('');
  const [username, setUsername] = useState('');
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const [lockAuth, setLockAuth] = useState(false);

  function setSuccessWithTimeout(val) {
    setSuccess(val);
    setTimeout(() => setSuccess(''), 3000);
  }

  function setErrorWithTimeout(val) {
    setError(val);
    setTimeout(() => setError(''), 3000);
  }

  function checkAuth() {
    fetch('/api/auth', { credentials: 'include' }).then((res) => {
      if (auth !== (res.status === 200)) {
        setAuth(res.status === 200);
      }
      return res.json().then((res) => {
        setHcaptchaSiteKey(res.hcaptchaSiteKey)
        if (res.username !== undefined && username !== res.username) {
          setUsername(res.username);
        }
      });
    });
  }

  function logout() {
    fetch('/api/logout', { credentials: 'include' })
      .then((res) => setAuth(false))
      .then(history.push({ pathname: '/', search: window.location.search }));
  }

  function GetCssHref() {
    const params = new URLSearchParams(window.location.search);
    const css = params.get('css');
    if (css !== null) {
      return '/api/getcss/' + css;
    }
    return '';
  }

  useEffect(() => {
    if (lockAuth) {
      return;
    }
    setLockAuth(true);
    checkAuth();
  }, [auth, username, lockAuth]);

  return (
    <div className="App">
      {window.location.search !== '' && (
        <link rel="stylesheet" type="text/css" href={GetCssHref()}></link>
      )}
      <Nav>
        <Nav.Item>
          <Nav.Link as={Link} to={{ pathname: '/', search: window.location.search }} id="home">
            Home
          </Nav.Link>
        </Nav.Item>
        {!auth && [
          <Nav.Item key="registrati">
            <Nav.Link
              as={Link}
              to={{ pathname: '/registrati', search: window.location.search }}
              id="registrati"
            >
              Registrati
            </Nav.Link>
          </Nav.Item>,
          <Nav.Item key="login">
            <Nav.Link
              as={Link}
              to={{ pathname: '/login', search: window.location.search }}
              id="login"
            >
              Login
            </Nav.Link>
          </Nav.Item>
        ]}
        {auth && [
          <Nav.Item key="logout">
            <Nav.Link onClick={logout}>Logout</Nav.Link>
          </Nav.Item>,
          <Nav.Item key="modifica-stile">
            <Nav.Link
              as={Link}
              to={{ pathname: '/modifica-stile', search: window.location.search }}
              id="modifica-stile"
            >
              Modifica Stile
            </Nav.Link>
          </Nav.Item>
        ]}
      </Nav>
      <Container>
        {error !== '' && <Alert variant="danger">{error}</Alert>}
        {success !== '' && <Alert variant="primary">{success}</Alert>}
        <Switch>
          <Route path="/login">
            <Login
              is_login={true}
              checkAuth={checkAuth}
              setSuccess={setSuccessWithTimeout}
              setError={setErrorWithTimeout}
            />
          </Route>
          <Route path="/registrati">
            <Login
              is_login={false}
              checkAuth={checkAuth}
              setSuccess={setSuccessWithTimeout}
              setError={setErrorWithTimeout}
            />
          </Route>
          <Route path="/modifica-stile">
            <ModificaStile
              setSuccess={setSuccessWithTimeout}
              setError={setErrorWithTimeout}
              username={username}
              hcaptchaSiteKey={hcaptchaSiteKey}
            />
          </Route>
          <Route path="/">
            <h1>Bevenuto nel mio nuovo blog!</h1>
            <img
              className="img-center"
              src="/Gabibbo_con_sguardo_truce_e_coltelli.jpg"
              alt="gabibbo"
            ></img>
            <p>
              Il sito è ancora in costruzione, non sono riuscito a trovare nessun buon designer, per
              questo ho fatto in modo che chiunque possa creare uno stile per la pagina, quindi
              registratevi bella gente! E fatemi vedere come pensate che il sito debba sembrare,
              guarderò subito tutte le vostre idee!
            </p>
          </Route>
        </Switch>
      </Container>
    </div>
  );
}
