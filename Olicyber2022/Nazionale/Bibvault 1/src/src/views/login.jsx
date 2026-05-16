const Main = require('./main');

<Main>
    <div className='container'>
        <h1>Login/Registrazione</h1>
        <p>Inserisci le tue credenziali e scegli se registrarti o fare il login</p>
        <form action="/login" method='POST'>
            <div class="form-group">
                <label>Username</label>
                <input type="text" className='form-control' name='username' required placeholder='username' />
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" className='form-control' name='password' required placeholder='password' />
            </div>
            <input type="submit" className='btn btn-primary' name="submit" value="Registrati" />
            <input type="submit" className='btn btn-primary' name="submit" value="Login" />
        </form>
    </div>
</Main>