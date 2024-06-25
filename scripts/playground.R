library(dplyr)
library(ggplot2)
library(httr)
library(jsonlite)

server_ip <- ""
base_url <- paste0("http://", server_ip, ":80")

response_req <- GET(paste0(base_url, "/responses"))
responses <-  content(stop_for_status(response_req)) |>
  bind_rows()

garbage <- responses |>
  group_by(prolific_id) |>
  mutate(n_id = n()) |>
  ungroup() |>
  filter(garbage) |>
  mutate(
    repeat_prolific_id = n_id >= 2,
    not_in_usa = !in_usa,
    not_committed = commitment %in% c("no", "unsure"),
    bad_captcha = tolower(captcha) != "purple",
    bad_attention_check = option_attention_truth != option_attention
  ) |>
  rowwise() |>
  mutate(anything_wrong = any(repeat_prolific_id:bad_attention_check)) |>
  ungroup()

cur_batch_req <- GET(paste0(base_url, "/bandit/batch/current?deactivate=False"))
cur_batch <- content(stop_for_status(cur_batch_req))$id

batch_req <- GET(paste0(base_url, "/bandit/batch"))
batch <- content(stop_for_status(batch_req))

pi_values <- bind_rows(
  lapply(
    batch,
    \(x) {
      batch_id = x[["batch"]][["id"]]
      parameters <- lapply(
        x[["parameters"]],
        \(y) {
          list(
            "arm_id" = y[["arm_id"]],
            "alpha" = y[["alpha"]],
            "beta" = y[["beta"]]
          )
        }
      )
      return(bind_rows(parameters) |> mutate(batch_id = batch_id))
    }
  )
)

pi_values_latest <- pi_values |>
  filter(batch_id == max(batch_id)) |>
  arrange(desc(arm_id)) |>
  rowwise() |>
  reframe(
    batch_id = batch_id,
    arm_id = factor(arm_id, levels = 1:16, ordered = TRUE),
    support = seq(0, 1, by = 0.001),
    pr = dbeta(support, alpha, beta)
  )

ggplot(
  pi_values_latest,
  aes(x = support, y = pr, color = factor(arm_id), group = arm_id)) +
  geom_line() +
  scale_color_manual(values = c(
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
    "#bcbd22", "#17becf", "#aec7e8", "#ffbb78",
    "#98df8a", "#ff9896", "#c5b0d5", "#c49c94"
  )) +
  coord_cartesian(xlim = c(0.3, 0.9)) +
  labs(
    x = "Support",
    y = "Density",
    title = "Posterior PDFs for Bandit Arms",
    color = ""
  ) +
  theme(
    panel.grid = element_line(color = "gray90"),
    panel.background = element_rect(fill = "white"),
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.title = element_text(face = "bold"),
    legend.title = element_text(face = "bold")
  )
