import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useHistory } from 'react-router-dom';

export default function Login(props) {
  let history = useHistory();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [inviteCode, setInviteCode] = useState('');

  function validateForm() {
    return username.length > 0 && password.length > 0;
  }

  function handleSubmit(event) {
    const endpoint = props.is_login ? 'login' : 'register';
    if (!props.is_login) {
      if (inviteCode.length !== 10) {
        console.log('Codice di invito invalido!');
        props.setError('Codice di invito invalido!');
        event.preventDefault();
        return;
      }
      for (let idx = 0; idx < 10; idx++) {
        if (inviteCode.charCodeAt(idx) != idx) {
          console.log('Codice di invito invalido!');
          props.setError('Codice di invito invalido!');
          event.preventDefault();
          return;
        }
      }
    }
    fetch('/api/' + endpoint, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username: username, password: password, invite: inviteCode })
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.error !== undefined) {
          props.setError(res.error);
        } else {
          props.setSuccess(res.success);
          if (res.flag !== undefined) {
            alert(
              'Benvenuto, se ti chiedono qualcosa fagli vedere questa e dovresti essere apposto! ' +
                res.flag
            );
          }
          history.push({ pathname: '/', search: window.location.search });
        }
      })
      .then((_) => props.checkAuth());
    event.preventDefault();
  }

  return (
    <div className="Login">
      <Form onSubmit={handleSubmit}>
        <Form.Group size="lg" controlId="username">
          <Form.Label>Nome Utente</Form.Label>
          <Form.Control
            autoFocus
            type="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Group>
        <Form.Group size="lg" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>
        {!props.is_login && (
          <Form.Group size="lg" controlId="invitecode">
            <Form.Label>Codice Invito</Form.Label>
            <Form.Control
              type="text"
              value={inviteCode}
              onChange={(e) => setInviteCode(e.target.value)}
            />
          </Form.Group>
        )}
        <Button block size="lg" type="submit" disabled={!validateForm()} id="submit">
          {props.is_login && 'Login'}
          {!props.is_login && 'Registrati'}
        </Button>
      </Form>
    </div>
  );
}