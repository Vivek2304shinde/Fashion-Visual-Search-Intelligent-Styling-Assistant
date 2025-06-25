// src/api/search.ts
export interface SearchResult {
    product_id: string;
    product_name: string;
    brand: string;
    price: number;
    image_url: string;
    product_url?: string;
    source?: string;
    similarity?: number;
}

export const uploadImage = async (file: File): Promise<SearchResult[]> => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:8000/api/v1/search', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.results;
    } catch (error) {
        console.error('Error uploading image:', error);
        throw error;
    }
};

export const searchByText = async (query: string): Promise<SearchResult[]> => {
    console.log("API CALL: Starting search for", query); // Add this
    try {
        const response = await fetch('http://localhost:8000/search/text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query.trim(),
                top_k: 30
            }),
        });
        console.log("API RESPONSE STATUS:", response.status); 
        if (!response.ok) {
            const errorData = await response.json();
            console.log("API ERROR:", errorData);
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("API SUCCESS DATA:", data);
        return data.results;
    } catch (error) {
        console.error('Error searching by text:', error);
        throw error;
    }
};