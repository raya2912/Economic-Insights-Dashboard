import plotly.express as px
import plotly.graph_objects as go

# Professional Fintech Color Palette
COLORS = {
    'primary': '#636EFA',
    'secondary': '#EF553B',
    'accent1': '#00CC96',
    'accent2': '#AB63FA',
    'background': 'rgba(0,0,0,0)',
    'text': '#E0E0E0',
    'grid': '#333333'
}

def apply_custom_theme(fig):
    fig.update_layout(
        plot_bgcolor=COLORS['background'],
        paper_bgcolor=COLORS['background'],
        font=dict(color=COLORS['text'], family="Inter, sans-serif"),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(showgrid=True, gridcolor=COLORS['grid'], linecolor=COLORS['grid'], zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=COLORS['grid'], linecolor=COLORS['grid'], zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title_text=''),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1E1E2D", font_size=13, font_family="Inter")
    )
    return fig

def create_line_chart(df, x_col, y_col, color_col, title, y_title):
    fig = px.line(df, x=x_col, y=y_col, color=color_col, title=title, markers=True,
                  color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent1'], COLORS['accent2']])
    fig.update_traces(line=dict(width=3), marker=dict(size=6), mode='lines+markers')
    fig.update_layout(yaxis_title=y_title, xaxis_title="")
    return apply_custom_theme(fig)

def create_bar_chart(df, x_col, y_col, color_col, title, y_title):
    fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=title, barmode='group',
                 color_discrete_sequence=[COLORS['accent1'], COLORS['primary'], COLORS['secondary']])
    fig.update_layout(yaxis_title=y_title, xaxis_title="")
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return apply_custom_theme(fig)

def create_heatmap(df, x_col, y_col, z_col, title):
    pivot_df = df.pivot(index=y_col, columns=x_col, values=z_col)
    fig = px.imshow(pivot_df, title=title, aspect="auto", color_continuous_scale="Viridis")
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return apply_custom_theme(fig)

def create_choropleth(df, locations, locationmode, color_col, title):
    fig = px.choropleth(df, locations=locations, locationmode=locationmode, color=color_col,
                        title=title, color_continuous_scale="Viridis", hover_name=locations)
    fig.update_layout(geo=dict(bgcolor=COLORS['background'], showframe=False, showcoastlines=True, coastlinecolor=COLORS['grid']))
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    return apply_custom_theme(fig)
