const Main = require('./main');

<Main>
    <div className='container'>
        <h1>Lista files</h1>
        <p>Qui puoi visionare i file che hai scaricato fino ad ora, inserisci un'url per scaricarlo</p>
        <form action="/files" method='POST'>
            <input type="text" className='form-control' name='url' required placeholder='http://example.com/?example=1' />
            <input type="submit" className='btn btn-primary' value="Scarica files" />
        </form>
        <div className='row'>
            {files.map(file => <div className="card" style={{width: "18rem"}}>
                    <div className="card-body">
                        <h5 className="card-title">{file}</h5>
                        <a href={`/download/?fileName=${file}`} className="btn btn-primary">Download</a>
                    </div>
            </div>)}

        </div>
    </div>
</Main>