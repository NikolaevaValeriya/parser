

library(shiny)
library(dplyr)
library(tidymodels)
library(readr)
library(ggplot2)
library(DT)

mean_metrics = read.csv("gen_all.csv")
mean_metrics = select(mean_metrics, -X)
top_metrics = read.csv('~/scraping/gen_top.csv')
top_metrics = select(top_metrics, -X, -country)

# Define UI for application that draws a histogram
ui <- fluidPage(

   # Application title
    titlePanel("Мир без границ"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
              selectInput("varnames",
                          "Выберите переменные для анализа",
                          choices = names(mean_metrics)[c(9:21)],  
                          multiple = TRUE),
      
              uiOutput('go') 
              
        ),

        # Show a plot of the generated distribution
        mainPanel(
          plotOutput('distplot'),
          dataTableOutput('table')
        )
      )
    )
# Define server logic required to draw a histogram
server <- function(input, output) {
    output$go = renderUI({
      numb = length(input$varnames)
      print(numb)
      elements <- lapply(1:numb, function(i){
        numericInput(paste0('weight', i),
                     paste0("Выберите вес для переменной:", i),
                     min = 0,
                     max = 1/(length(input$varnames)),
                     value = 1/(length(input$varnames))) 
      })
      return(elements)
    })
       output$distplot <- renderPlot({
          mean_metrics <- mean_metrics %>% mutate(y = 0)
          
          for(i in 1:length(input$varnames)) {
          mean_metrics = mean_metrics %>% mutate(y =  y + mean_metrics[[input$varnames[i]]] * input[[paste0('weight', i)]])}
          ggplot(data = mean_metrics, aes(x = city, y = y, fill = country)) +
            geom_bar(stat="identity", color="black")+
            theme(axis.text.x=element_text(angle=60, vjust=0.4, size = 12))+
            xlab("Название города")+
            ylab("Балльная оценка")+
            ggtitle("Рейтинг городов в зависимости от потребностей путешественника")+
            theme(axis.title.x=element_text(vjust=-0.7))
          })
       output$table <- renderDataTable(
         top_metrics,
         options = list(
           pageLength = 5,
           initComplete = I("function(settings, json) {alert('Done.');}")
       )
       )
       
       }

# Run the application 
shinyApp(ui = ui, server = server)
