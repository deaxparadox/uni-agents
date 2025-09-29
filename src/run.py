import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "backend.asgi:application",         
        host="0.0.0.0",    
        port=9009,
        reload=True,         
        log_level="debug",   
        workers=1,
        lifespan="on"            
    )
