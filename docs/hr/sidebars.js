// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  useCasesSidebar: [{ type: 'autogenerated', dirName: 'use_cases' }],

  tutorialSidebar: [
    {
      type: 'doc',
      label: 'Welcome',
      id: 'docs/intro',
    },
    {
      type: 'doc',
      label: 'FAQ',
      id: 'docs/faq',
    },
    {
      type: 'category',
      label: 'Get started',
      collapsed: true,
      collapsible: true,
      items: [
        'docs/get_started/installation',
        'docs/get_started/configuration',
        'docs/get_started/environment',
        'docs/get_started/hello_world',
      ],
      link: {
        type: 'doc',
        id: 'docs/get_started/first_steps',
      },
    },
    {
      type: 'category',
      label: 'Core API',
      link: {
        type: 'doc',
        id: 'docs/core_api/intro',
      },
      items: [
        'docs/core_api/connect',
        'docs/core_api/apply',
        'docs/core_api/execute',
      ]
    },
    {
      type: 'category',
      label: 'Apply API',
      link: {
        type: 'doc',
        id: 'docs/apply_api/component',
      },
      items: [
        'docs/apply_api/model',
        'docs/apply_api/listener',
        'docs/apply_api/vector_index',
        'docs/apply_api/stack',
        'docs/apply_api/datatype',
        'docs/apply_api/schema',
        'docs/apply_api/table',
        'docs/apply_api/dataset',
        'docs/apply_api/metric',
        'docs/apply_api/validation',
        'docs/apply_api/checkpoint',
        'docs/apply_api/trainer',
      ]
    },
    {
      type: 'category',
      label: 'Execute API',
      link: {
        type: 'doc',
        id: 'docs/execute_api/overview',
      },
      items: [
        'docs/execute_api/overview',
        {
          type: 'category',
          label: 'Inserting data',
          link: {
            type: 'doc',
            id: 'docs/execute_api/inserting_data',
          },
          items: [
            'docs/execute_api/data_encodings_and_schemas',
            'docs/execute_api/encoding_special_data_types',
            'docs/execute_api/using_hybrid_storage_to_handle_large_data_blobs',
            'docs/execute_api/referring_to_data_from_diverse_sources',
          ]
        },
        {
          type: 'category',
          label: 'Selecting data',
          link: {
            type: 'doc',
            id: 'docs/execute_api/select_queries',
          },
          items: [
            'docs/execute_api/mongodb_queries',
            'docs/execute_api/ibis_queries',
            'docs/execute_api/sql_native_queries',
          ]
        },
        {
          type: 'category',
          label: 'Vector search',
          link: {
            type: 'doc',
            id: 'docs/execute_api/vector_search',
          },
          items: [
            'docs/execute_api/setting_up_vector_search',
            'docs/execute_api/native_vector_search',
            'docs/execute_api/lance_index_vector_search',
            'docs/execute_api/vector_search_queries',
          ]
        },
        'docs/execute_api/update_queries',
        'docs/execute_api/delete_queries',
        'docs/execute_api/predictions',
      ]
    },
    {
      type: 'category',
      label: 'Models',
      link: {
        type: 'doc',
        id: 'docs/models/ai_models',
      },
      items: [
        {type: 'autogenerated', dirName: 'docs/models'},
      ]
    },
    {
      type: 'category',
      label: 'Reusable snippets',
      collapsed: true,
      collapsible: true,
      items: [
        'docs/reusable_snippets/connect_to_superduperdb',
        'docs/reusable_snippets/create_datatype',
        'docs/reusable_snippets/get_useful_sample_data',
        'docs/reusable_snippets/insert_data',
        'docs/reusable_snippets/compute_features',
        'docs/reusable_snippets/build_text_embedding_model',
        'docs/reusable_snippets/build_image_embedding_model',
        'docs/reusable_snippets/build_multimodal_embedding_models',
        'docs/reusable_snippets/build_llm',
        'docs/reusable_snippets/finetune_llm',
        'docs/reusable_snippets/create_vector_index',
        'docs/reusable_snippets/perform_a_vector_search',
        'docs/reusable_snippets/connecting_listeners',
        'docs/reusable_snippets/build_and_train_classifier',
      ],
      link: {
        type: 'generated-index',
        description: 'Common patterns for quick use',
      },
    },
    {
      type: 'category',
      label: 'Data integrations',
      collapsed: false,
      link: {
        type: 'doc',
        id: 'docs/data_integrations/intro',
      },
      items: [
        'docs/data_integrations/mongodb',
        {
          type: 'category',
          label: 'SQL Databases',
          collapsed: false,
          link: {
            type: 'doc',
            id: 'docs/data_integrations/sql',
          },
          items: [
            'docs/data_integrations/mysql',
            'docs/data_integrations/postgresql',
            'docs/data_integrations/snowflake',
            'docs/data_integrations/sqlite',
            'docs/data_integrations/duckdb',
          ]
        },
        'docs/data_integrations/pandas', 
      ]
    },
    {
      type: 'category',
      label: 'AI integrations',
      collapsed: false,
      link:{
        type: 'generated-index',
        title: 'AI Integrations',
        description:
          "Learn more about our AI Integrations which consists of AI models, AI APIs and Frameworks",
      },
      items: [
        'docs/ai_integrations/anthropic',
        'docs/ai_integrations/cohere',
        'docs/ai_integrations/custom',
        'docs/ai_integrations/jina',
        'docs/ai_integrations/llm',
        'docs/ai_integrations/openai',
        'docs/ai_integrations/pytorch',
        'docs/ai_integrations/sklearn',
        'docs/ai_integrations/transformers',
      ]
      
    },
    {
      type: 'category',
      label: 'Fundamentals',
      link: {
        type: 'doc',
        id: 'docs/fundamentals/glossary',
        
      },
      items: [
        'docs/fundamentals/glossary',
        'docs/fundamentals/design',
        'docs/fundamentals/datalayer_overview',
        'docs/fundamentals/document_encoder_abstraction',
        'docs/fundamentals/serializables',
        'docs/fundamentals/component_abstraction',
        'docs/fundamentals/component_versioning',
        'docs/fundamentals/declarative_api',
        'docs/fundamentals/predictors_and_models',
        'docs/fundamentals/vector_search_algorithm',
      ]
    },
    // {
    //   type: 'category',
    //   label: 'How To',
    //   link: {
    //     type: 'doc',
    //     id: 'docs/walkthrough/tutorial_walkthrough',
    //   },
    //   items: [
    //     'docs/setup/connecting',
    //     'docs/walkthrough/data_encodings_and_schemas',
    //     'docs/walkthrough/inserting_data',
    //     'docs/walkthrough/referring_to_data_from_diverse_sources',
    //     'docs/walkthrough/using_hybrid_storage_to_handle_large_data_blobs',
    //     'docs/walkthrough/selecting_data',
    //     'docs/walkthrough/ai_models',
    //     'docs/walkthrough/training_models',
    //     'docs/walkthrough/apply_models',
    //     'docs/walkthrough/linking_interdependent_models',
    //     'docs/walkthrough/vector_search',
    //     'docs/walkthrough/serialization',
    //     'docs/walkthrough/creating_stacks_of_functionality',
    //   ],
    // },
    {
      type: 'category',
      label: 'Production features',
      items: [
        {
          type: 'autogenerated',
          dirName: 'docs/production',
        },
      ],
    },
    {
      type: 'category',
      label: 'Use cases',
      collapsed: true,
      collapsible: true,
      items: [{ type: 'autogenerated', dirName: 'use_cases' }],
      link: {
        type: 'generated-index',
        description:
          'Common and useful use-cases implemented in SuperDuperDB with a walkthrough',
      },
    },

    {
      type: 'category',
      label: 'Reference',
      items: [
        {
          type: 'link',
          label: 'API Reference', // The link label
          href: 'https://docs.superduperdb.com/apidocs/source/superduperdb.html', // The external URL
        },
        {
          type: 'link',
          label: 'Change log', // The link label
          href: 'https://raw.githubusercontent.com/SuperDuperDB/superduperdb/main/CHANGELOG.md', // The external URL
        },
      ],
    },
  ],
};

module.exports = sidebars;
