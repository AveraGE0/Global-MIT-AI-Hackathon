from langchain.prompts import PromptTemplate


def video_creating_prompt():
    prompt_template = PromptTemplate(
            input_variables=["brand_name", "product", "tone", "trend_description"],
            template="""
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Write a vivid, two-sentence text-to-video prompt (max 80 words) that showcases brand and  product in a tone style inspired by trend_description, 
    using strong visual storytelling and metaphor.Include the brand name, 
    maintain consistent brand identity, and avoid introductory phrases, trend labels (e.g. “Trend:…”), and all hashtags.
    Important:
    use the brandname in the output and mention the product
    Based on the trend description make detailed prompt so it can be used by pika api to create a video
    Do not include an Introduction sentence like: Here is a two-sentence text-to-video prompt that showcases the Starbucks brand and container product in a tone style inspired by Italian Brainrot
    Only Output the prompt nothing else
    <|eot_id|><|start_header_id|>user<|end_header_id|>

    {brand_name}
    {product}
    {tone}
    {trend_description}

    <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """
        )
    return prompt_template


def create_hashtags():
    prompt_template_hastags = PromptTemplate(
        input_variables=["brand_name","product", "hashtags","tone"],
        template= """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Suggest a mix of trending, niche, and brand-relevant hashtags for the brand, targeted at a specific target  
    Use a tone, and take inspiration from the following reference hashtags.
    Give out list of 6 hashtags
    
    Important: 
    Do Not use an Instruction prompt 
    Do not output: <|eot_id|>
    Do not output anything else!
    The output should look like that: 
    #1, #2, #3, #4, #5, #6
    
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    
    {brand_name}
    {hashtags}
    {product}
    {tone}

    
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """)

    return prompt_template_hastags


def create_caption():
    prompt_template_caption  = PromptTemplate(
        input_variables = ["brand_name","product","tone"],
        template = """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    Do not start your text with "
    Write a short, engaging social media caption for the brand  tailored to appeal to the target audience 
    Use a tone. Integrate the following hashtags naturally 
    Do not make an Introduction sentence like:  Here is a two-sentence text-to-video prompt:
    Important the brand name needs to be in the text
    Incoperate #brandname
    Keep it under 30 words and make it attention-grabbing, aligned with current trends and brand identity.

    <|eot_id|><|start_header_id|>user<|end_header_id|>
    
    {brand_name}
    {product}
    {tone}

    
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>  
    """
    )
    return prompt_template_caption


def prediction_forecast():
    prompt_template_caption = PromptTemplate(
        input_variables=["brand_name", "product","caption", "hashtags"],
        template="""
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are an Evaluation Assistant.

    You are provided with the following:
    - Brand: brand_name
    - Product: product
    - Caption: caption
    - Hashtags: hashtags
    
    Your task is to evaluate how impactful this social media post is likely to be.
    
    Assess how well the caption and hashtags align with current trends and brand identity.
    Respond with a brief, 2–3 sentence explanation of the post’s engagement potential.
    
    Do not begin with a quotation mark.
    Do not include phrases like "Here is..." or "This is a...".


    <|eot_id|><|start_header_id|>user<|end_header_id|>

    {brand_name}
    {product}
    {hashtags}
    {caption}


    <|eot_id|><|start_header_id|>assistant<|end_header_id|>  
    """
    )
    return prompt_template_caption

