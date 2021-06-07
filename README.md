# CRM_CONSIG_DJANGO
Repositório do projeto DJANGO para o CRM Consig


## Instruções para deploy

O CRM está em um servidor com Ubuntu 18:04 os arquivos desse projeto se encontram em duas pasta
que são


    /home/alldigital/prod
    /home/alldigital/dev
    
Sendo a pasta dev como ambiente em desenvolvimento. O Ambiente de desensolvimento está rodando no ip http://148.72.153.72/
Para restart a aplicação em ambiente de produção execute o comando:


    sudo systemctl restart dev-gunicorn.service
  
Já a pasta de prod, roda a aplicação em produção e ela está atende o dominio http://gobank.digital
Para restart a aplicação o comando é: 

    sudo systemctl restart prod-gunicorn.service
    
Caso sinta necessidade de reiniciar o servidor http Nginx rode o comando


      sudo systemctl restart nginx
      
A configuração do Nginx fica em /etc/nginx/sites-avaibles tendo dois arquivos de configuração
para cada ambiente, mais o arquivo default que não precisa ser mexido.



        
     

