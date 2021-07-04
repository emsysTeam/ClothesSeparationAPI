Django web publish

# Kim Kyeong Jun


### 실행

```
docker-compose up
```

### 백그라운드 실행

```
docker-compose up -d
```

### 코드 수정 후 실행(docker, nginx 이미지 새롭게 빌드)

```
docker-compose up --build
```


### 종료

```
docker-compose down -v
```



### 개발 및 배포 CI/CD 파이프라인

![pipeline](https://user-images.githubusercontent.com/50234590/124381001-26c0be80-dcfb-11eb-983f-40a8c14a34d0.PNG)
