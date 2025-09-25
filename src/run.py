import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "backend.asgi:application",         
        host="127.0.0.1",    
        port=9000,
        reload=True,         
        log_level="debug",   
        workers=1,
        lifespan="on"            
    )
